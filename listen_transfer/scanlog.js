const celery = require('celery-node');
const Web3 = require('web3');
const _ = require('lodash');
const delay = require('delay');

require('dotenv').config()
let Block = 32534790;
const Rpc = ["https://bsc.blockpi.network/v1/rpc/public", "https://bsc-rpc.gateway.pokt.network", "https://bsc.rpc.blxrbdn.com", "https://bsc-dataseed2.binance.org"];

async function makeTopicData({log, httpWeb3}){

    const topics = _.get(log, 'topics')
    const fromadd = httpWeb3.eth.abi.decodeParameter(
        'address',
        topics[1]
      )
      const toadd = httpWeb3.eth.abi.decodeParameter(
        'address',
        topics[2]
      )

      const eventType = [
        {
            "indexed": false,
            "internalType": "uint256",
            "name": "Ammount",
            "type": "uint256"
          }
       
    ];
    const a = log.data 
    const parseData = httpWeb3.eth.abi.decodeParameters(
        eventType,
        a,
    );
    const txhash =log.transactionHash


      let args = {}
      args.fromadd =fromadd
      args.toadd =toadd
      args.ammount =parseData.Ammount
      args.txhash =txhash
      if(fromadd!="0x0000000000000000000000000000000000000000"){
        console.log(args)
      
        const celeryClient = await celery.createClient(
            "redis://localhost:6379/0",
            "redis://localhost:6379/0",
            "tc-queue"
    
        );
        const celeryTask = celeryClient.createTask("worker.transfertoken")
        console.log(celeryTask)
        await celeryTask.delay({args:args});
      }
    
      



}
async function makeEventData({log, eventType, httpWeb3}){
    const a = log.data 
    const parseData = httpWeb3.eth.abi.decodeParameters(
        eventType,
        a,
    );
    let args = {}
    args.owner =parseData.owner_minted
    args.rank =parseData.rank
    args.time_minted =parseData.time_minted
    const topics = _.get(log, 'topics')

    const tokenId = httpWeb3.eth.abi.decodeParameter(
        'uint256',
        topics[1]
      )
    args.tokenId = tokenId
    console.log(args)

     const celeryClient = await celery.createClient(
        process.env.REDIS_URL,
        process.env.REDIS_URL,
        "tc-queue"

    );
    console.log(celeryClient)
    const celeryTask = celeryClient.createTask("worker.mintNft")
    console.log(celeryTask)
    await celeryTask.delay({args:args});
}
async function handleLog(log, httpWeb3){

    await makeTopicData({
        log,
        httpWeb3

    });
}


async function scanLog({fromBlock}){
    rpc = Rpc[0]
    console.log(rpc)
    httpWeb3 = new Web3(rpc)
    const latestBlock = await httpWeb3.eth.getBlockNumber();
    console.log(latestBlock)
    while(fromBlock<latestBlock){
        var toBlock =0;
        if(fromBlock +20 >latestBlock){
            toBlock = latestBlock

        }
        else{
            toBlock = fromBlock + 20
        }
        console.log(`Scan from ${fromBlock}, to ${toBlock}, lastest: ${latestBlock}`)
        const logs = await httpWeb3.eth.getPastLogs({
            fromBlock,
            toBlock,
            topics:["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"],
            address:["0x0927dbfe1bb5b31e41031cb4db2a8c20115b3baa"]
        })
        for(let log of logs){
            const event = await handleLog(log,httpWeb3)
        }
        console.log("new block------------------------------------------------------------")
        fromBlock = toBlock
        Block =toBlock
    }
    await delay(15 * 1000)

}

async function start(){
    while (true){
    try{
       
            console.log("--------------------------Ddd------------------------------------------")
          
            const latestBlock =await scanLog({
                fromBlock:Block
            });
            console.log(Block)
    }catch(error){
        Rpc.push(Rpc[0])
        Rpc.shift()

    }


}



}

start();
