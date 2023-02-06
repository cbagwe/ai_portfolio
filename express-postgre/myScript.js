readTodos();
async function readTodos() {

    try{
        const companies_table = document.getElementById("companies_table");
        while(companies_table.firstChild) companies_table.removeChild(companies_table.firstChild);

        const result = await fetch("http://localhost:8080/prodCreation", {method:"GET"});
        const companies = await result.json();

        // create elements <table> and a <tbody>
        // var tbl = document.createElement("table");
        var tblBody = document.createElement("tbody");

        var header_values = ['ID', 'Company', 'Product', 'Cluster', 'Sub-Cluster', 'Website'];
        var header_row = document.createElement("tr");
        header_row.setAttribute('id','header-row');

        for (var i = 0; i < 6; i++)
        {
            var cell = document.createElement("th");
            var t_value = document.createTextNode(header_values[i]);
            cell.setAttribute('id',header_values[i]);
            cell.appendChild(t_value);
            header_row.append(cell);
        }

        tblBody.appendChild(header_row);

        // cells creation
        companies.forEach(t=>{
            // table row creation
            var row = document.createElement("tr");
            var values = Object.values(t);

            for (var i = 0; i < 6; i++)
            {
                var cell = document.createElement("td");

                if(i == 5)
                {
                    var a = document.createElement("a");
                    var linkText = document.createTextNode("Link");
                    a.appendChild(linkText);
                    a.title = "Link";
                    a.href = values[i];
                    cell.appendChild(a);
                }
                else{
                    var t_value = document.createTextNode(values[i]);
                    cell.appendChild(t_value);
                }
                row.append(cell);
            }
            tblBody.appendChild(row);
        })

        // append the <tbody> inside the <table>
        companies_table.appendChild(tblBody);
    }
    catch (e) {
        console.log("Error reading the companies.");
    }

}