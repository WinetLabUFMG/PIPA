import {Link} from 'react-router-dom';
import styles from './Navbar.module.css'
import { useNavigate } from 'react-router-dom';


function Navbar(){

    return (
 
    <div>
     <nav className={styles.navbar}>     
            <h1 style={{color: 'white', padding: '0.5em'}}>PIPA</h1>
        
        <ul className={styles.list}>
            <li className={styles.item}><Link to="/home">Home</Link></li>
            <li className={styles.item}><Link to="/cadastro">Fomulário Cadastro</Link></li>
            <li className={styles.item}><Link to="/usuarios">Usuários</Link></li>
            <li className={styles.item}><Link to="/politicas">Grupos</Link></li>
            <li className={styles.item}><Link to="/perfil">Perfil</Link></li>
        </ul>

        </ nav>

        <br></br>
    </div>

    )
}

export default Navbar