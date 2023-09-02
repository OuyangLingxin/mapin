function MyComponent() {
  const [emps, setEmp] = React.useState([]);
  React.useEffect(() => {
    fetch('/employee')
      .then(response => response.json())
      .then(data => {
          setEmp(data)
      });
  }, []);

  // console.log(emps)
  const empList = []
  for(const emp of emps){
    empList.push(
      <div key={emp.id}>
        Employee ID: <b>{emp.id}</b>,
        Employee Name: <b>{emp.name}</b>,
        Employee Cell: <b>{emp.cell}</b>
      </div>
    );
  }
  return (
    <div>
      {empList}
    </div>
  );
};


ReactDOM.render(<MyComponent />, document.querySelector('#grid'))