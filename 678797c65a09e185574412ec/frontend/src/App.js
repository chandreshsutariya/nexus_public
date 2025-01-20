```javascript
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './components/Home';
import Upload from './components/Upload';
import FindPhotos from './components/FindPhotos';
import PasswordProtect from './components/PasswordProtect';
import Results from './components/Results';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/upload" component={Upload} />
          <Route path="/find-photos" component={FindPhotos} />
          <Route path="/password-protect" component={PasswordProtect} />
          <Route path="/results" component={Results} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
```