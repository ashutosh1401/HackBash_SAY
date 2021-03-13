import {BrowserRouter as Router,Route,Switch} from 'react-router-dom';
import './App.css';
import Home from './pages/Home/Home';
import LogIn from './pages/auth/Login';
import SignUp from './pages/auth/Signup';
function App() {
  return (
   <Router>
     <Switch>
       <Route path="/" exact={true} component={Home}></Route>
       <Route path="/login" exact={true} component={LogIn}></Route>
       <Route path="/signup" exact={true} component={SignUp}></Route>
     </Switch>
   </Router>
  );
}

export default App;
