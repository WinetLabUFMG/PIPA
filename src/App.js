import './App.css';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages/Home';
import FormularioCadastro from './pages/FormCadastro';
import Usuarios from './pages/Usuarios';
import Usuario from './pages/Usuario';
import Navbar from './layout/Navbar';
import Footer from './layout/Footer'
import GrupoPoliticas from './pages/GrupoPoliticas'
import GrupoPolitica  from './pages/GrupoPolitica'
import CriarGrupo from './pages/CriarGrupo';
import SolicitaçãoCadastramento from './pages/SolicitaçãoCadastramento';


function App() {
  return (

      <Router>
       <div className='AppContainer'>
        <Navbar />

        <Routes>
          <Route path="/" index element={<SolicitaçãoCadastramento/>} ></Route>
          <Route path="/home" index element={<Home/>} ></Route>
          <Route path="cadastro" element={<FormularioCadastro/>}></Route>
          <Route path="usuarios" element={<Usuarios/>}></Route>
          <Route path="usuario/:username" element={<Usuario/>}></Route>
          <Route path="politicas" element={<GrupoPoliticas/>}></Route>
          <Route path="politica/:policyID" element={<GrupoPolitica/>}></Route>
          <Route path="criargrupo" element={<CriarGrupo/>}></Route>


        </Routes>

        <Footer />
      </div>
      </Router>
  );
}

export default App;
