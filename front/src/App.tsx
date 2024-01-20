import React from 'react';
import './App.css';
import ArtifactSelect from './ArtifactSelect';
import DisplayLocations from './DisplayLocations';

import { Routes, Route, BrowserRouter } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="artifact">
          <Route path=":runId" element={<ArtifactSelect selectedArtifact='125' />} />
        </Route>
      </Routes>
    </BrowserRouter>

    // <div>
    //   <h2>ABR</h2>
    //   <ArtifactSelect selectedArtifact='2' />
    //   {/* <DisplayLocations />  */}
    // </div>
  );
}

export default App;
