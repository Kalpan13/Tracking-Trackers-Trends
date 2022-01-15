const puppeteer = require('puppeteer');
const PuppeteerHar = require('puppeteer-har');

async function create_har(website) {
  try{
  const browser = await puppeteer.launch();
    const page = await browser.newPage();

    const har = new PuppeteerHar(page);
    await har.start({ path: "captured_hars/"+website+'.har' });

    await page.goto('http://'+website);

    await har.stop();
    await page.close();
    await browser.close();
    console.log("Done : "+website)
    }   
  catch(e){
    console.log("Error : "+website);
    console.log("Error : "+e.stack);  
}
};

let fn = async(chunks) => {
    let curr;
    try {
      curr = await Promise.all(chunks.map(create_har));
    } catch(err) {
      throw err
    }
    if (curr !== undefined && websites.length)
        fn(websites.splice(0, 1));
  }

fn(websites.splice(0, 1))
.then()
.catch((err) => console.error(err))
