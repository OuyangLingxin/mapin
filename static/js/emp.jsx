function MyComponent() {
  const [emps, setEmp] = React.useState([]);
  let count = emps.length
  React.useEffect(() => {
    fetch('/employee')
      .then(response => response.json())
      .then(data => {
          setEmp(data)
      });
  }, [count]);

  // console.log(emps)
  const empList = []
  for(const emp of emps){
    empList.push(
          <a href={"/maps/"+emp.id}>
            <li>
            Employee ID: <b>{emp.id}</b>,
            Employee Name: <b>{emp.name}</b>,
            Employee Cell: <b>{emp.cell}</b>
            </li>
          </a>
    );
  }
  return (
    <div>
      {empList}
    </div>
  );
};


ReactDOM.render(<MyComponent />, document.querySelector('#grid'))