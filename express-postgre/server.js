//using pool is better for web apps so that we can 
//reserve a client connection for each request and 
//avoid problems with concurrent requests.. 
//Check out this video I discuss this in details
//https://www.youtube.com/watch?v=GTeCtIoV2Tw
//I Changed all the singelton clients in this code to Pool

const {Pool} = require("pg")
const express = require ("express")
const app = express();
app.use(express.json())

const pool = new Pool({
    "user": "postgres",
    "password" : "Chaitali@28",
    "host" : "127.0.0.1",
    "port" : 5432,
    "database" : "postgres"
})

 
app.get("/", (req, res) => res.sendFile(`${__dirname}/index.html`))
app.get("/myScript.js", (req, res) => res.sendFile(`${__dirname}/myScript.js`))

app.get("/prodCreation", async (req, res) => {
    const rows = await readProdCreationCompanies();
    res.setHeader("content-type", "application/json")
    res.send(JSON.stringify(rows))
})


app.listen(8080, () => console.log("Web server is listening.. on port 8080"))

start()

async function start() {
    await connect();
}

async function connect() {
    try {
        await pool.connect(); 
    }
    catch(e) {
        console.error(`Failed to connect ${e}`)
    }
}

async function readProdCreationCompanies() {
    try {
    const results = await pool.query("select * from prodcreation_companies");
    return results.rows;
    }
    catch(e){
        return [];
    }
}