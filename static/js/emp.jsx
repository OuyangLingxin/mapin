function MyComponent() {
  const [emps, setEmp] = React.useState([]);
  let count = emps.length
  let val = emps.value
  React.useEffect(() => {
    fetch('/employee')
      .then(response => response.json())
      .then(data => {
          setEmp(data)
      });
  }, [count, val]);

  // console.log(emps)
  const empList = []
  for(const emp of emps){
    empList.push(
      <div className="border border-2 shadow-sm p-1 mb-3 --bs-body-bg-rgb rounded col-3 text-center d-inline-block">
          <a href={"/maps/"+emp.id} className="text-decoration-none text-black">
            {emp.name}
          </a>
          </div>
    );
  }
  return (
    <div>
      {empList}
    </div>
  );
};


ReactDOM.render(<MyComponent />, document.querySelector('.container #grid'))