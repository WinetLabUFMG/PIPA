import styles from './Home.module.css'
import { useNavigate } from 'react-router-dom'

import logo_mpmg from '../../img/Logo_mpmg.png'
import logo_ufmg from '../../img/logo_dcc.png';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2';

function Home(){

    const history = useNavigate()

    return (

       
        <div>
            <Box sx={{ flexGrow: 1}}>
                <Grid container spacing={2} columns={12}>

                    <Grid xs={6}>
                        <h1 className={styles.h1}> PIPA </h1>
                        <h4 className={styles.p}>
                            O PIPA (Plataforma Integrada de Políticas de Acesso) é uma plataforma de gerenciamento de autorização de serviços de autorização do 
                            ambiente computacional do GSI/MPMG
                        </h4>

                        <img className={styles .logoMPMG} src={logo_mpmg}></img>
                        <img className={styles.logoUFMG} src={logo_ufmg}></img>
                    
                    </Grid>

                    <Grid xs={6}>
                        <Grid container spacing={2} columns={6}>
                            <Grid xs={3}>

                                <div className={styles.Container}>
                                    <button className={styles.btn} onClick={() => history("/cadastro")}><h1>Cadastrar usuário</h1></button>
                                </div>

                                <div className={styles.Container}>
                                    <button className={styles.btn} onClick={() => history("/politicas")}><h1>Associar usuários a um grupo</h1></button>
                                </div>

                                

                            </Grid>

                            <Grid xs={3}>

                                <div className={styles.Container}>
                                    <button className={styles.btn} onClick={() => history("/criargrupo")}><h1>Criar grupo de políticas</h1></button>
                                </div>
                               

                                <div className={styles.Container}>
                                    <button className={styles.btn} onClick={() => history("/politicas")}><h1>Visualizar grupos</h1></button>
                                </div>

                            </Grid>
                        </Grid>
                    </Grid>
                    
                </Grid>
            </Box>
        </div>
        
    )
}

export default Home;