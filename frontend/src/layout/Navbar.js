import {Link} from 'react-router-dom';
import styles from './Navbar.module.css'
import userIcon from '../img/download.png'
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import { useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';

function Navbar(){
    const history = useNavigate()

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