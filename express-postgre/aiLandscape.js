readTodos();
async function readTodos() {

    try{
        //while(companies_div.firstChild) companies_div.removeChild(companies_div.firstChild);

        /*var iDiv = document.createElement('div');
        iDiv.id = 'spp-companies';
        iDiv.className = 'spp-companies';

        var innerDiv = document.createElement('div');
        innerDiv.className = 'idea-generation';*/

        const idea_generation_div = document.getElementById("idea-generation").parentNode;
        const customer_market_div = document.getElementById("customer-market-analysis").parentNode;
        const testing_div = document.getElementById("testing").parentNode;
        const requirements_management_div = document.getElementById("requirements-management").parentNode;
        const product_management_div = document.getElementById("product-management").parentNode;
        const product_design_div = document.getElementById("product-design").parentNode;
        const process_optimization_div = document.getElementById("process-optimization").parentNode;
        const maintenance_div = document.getElementById("maintenance").parentNode;

        const result = await fetch("http://localhost:8080/prodCreation", {method:"GET"})
        const companies = await result.json();


        // cells creation
        companies.forEach(t=>{
            // table row creation
            var values = Object.values(t);
            switch(values[4])
            {
                case "Idea Generation":
                    var company_div = createCompanyStruct(values[1], values[5]);
                    idea_generation_div.appendChild(company_div);
                    break;
                case "Customer Market Analysis":
                    var company_div = createCompanyStruct(values[1], values[5]);
                    customer_market_div.appendChild(company_div);
                    break;
                case "Testing":
                    var company_div = createCompanyStruct(values[1], values[5]);
                    testing_div.appendChild(company_div);
                    break;
                case "Requirements Management":
                    var company_div = createCompanyStruct(values[1], values[5]);
                    requirements_management_div.appendChild(company_div);
                    break;
                case "Product Management":
                    var company_div = createCompanyStruct(values[1], values[5]);
                    product_management_div.appendChild(company_div);
                    break;
                case "Product Design":
                    var company_div = createCompanyStruct(values[1], values[5]);
                    product_design_div.appendChild(company_div);
                    break;
                /*case "Process Optimization":
                    var company_div = createCompanyStruct(values[1], values[5]);
                    process_optimization_div.appendChild(company_div);
                    break;
                case "Maintenance":
                    var company_div = createCompanyStruct(values[1], values[5]);
                    maintenance_div.appendChild(company_div);
                    break;*/
                default:
                    break;
            }
        })

        /*iDiv.appendChild(innerDiv);
        companies_div.appendChild(iDiv);*/
    }
    catch (e) {
        console.log("Error reading the companies.")
    }

}

function createCompanyStruct(company_name, company_link) {
    var company_div = document.createElement("div");
    company_div.className = "landscape-company";
    var company = document.createElement("a");
    var linkText = document.createTextNode(company_name);
    company.appendChild(linkText);
    company.title = company_name;
    company.href = company_link;
    company_div.appendChild(company);
    return company_div;
}