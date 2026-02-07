document.addEventListener('DOMContentLoaded',function(){
       const form = document.getElementById('expense-form');
       const tbody = document.getElementById('expense-tbody');

       loadExpenses();

       form.addEventListener('submit',
        async function(e){
            e.preventDefault();

            const date = document.getElementById('date').value;
            const category = document.getElementById('category').value;
            const item_name = document.getElementById('item_name').value;
            const quantity = parseFloat(document.getElementById('quantity').value);
            const  price   = parseFloat(document.getElementById('price').value);
            const total = parseFloat(document.getElementById('total').value);
            
            const response = await fetch('/api/add-expense',{
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({date,category,item_name,quantity,price,total})
            });
            if (response.ok){
                const expenses=await response.json();
                renderTable(expenses);
                form.reset();
            }
        });
        async function loadExpenses(){
            const response = await fetch('/api/expenses');
            const expenses = await response.json();
            renderTable(expenses);
        }
        function renderTable(){
            tbody.innerHTML = '';
            expenses.forEach(element => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${element.date}</td>
                    <td> ${element.category}</td>
                    <td>${element.item_name}</td>
                    <td>${element.quantity}</td>
                    <td>${element.price}</td>
                    <td>${element.total}</td>`;
                    tbody.appendChild(row);}); 
        }
});
