import styles from './Perfil.module.css'
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import ReadMoreIcon from '@mui/icons-material/ReadMore';
import AddIcon from '@mui/icons-material/Add';
import Button from '@mui/material/Button';

function Perfil(){

    const navigate = useNavigate();

    const [perfil, setPerfil] = useState([])

    useEffect(() => {
        
        fetch('http://localhost:5000/userinfo',{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((resp) => resp.json())
            .then((data) => {
              setPerfil(data)
            })
            .catch((error)=> console.log(error))

    }, [])

    function Logout(){     
        document.cookie = 'authTRUE=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.replace("http://localhost:3000/");
    }

    return (
       
        <div className={styles.Perfil_container}>

                        
            <h1>Perfil</h1>
            
            <div >
                
                <div key={perfil.sub}>
                    <Accordion >
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="panel1a-content"
                            id="panel1a-header"

                            sx = {{
                                    borderBottomLeftRadius: '0.5em', 
                                    borderBottomRightRadius:'0.5em',
                                  }}
                        >
                             <Typography sx={{ fontWeight: 'bold', fontSize: 24 }}>{perfil.sub}</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <Typography>
                                <b>Usuário:</b> {perfil.sub}
                            </Typography>

                            <Typography>
                                <br></br>
                                <b>WSO2 email:</b> {perfil.email}
                            </Typography>
                                    <br></br>

                            <Button onClick={() => {Logout()}} variant="outlined" startIcon={<ReadMoreIcon />}>
                                Log Out
                            </Button>
                        </AccordionDetails>
 
                    </Accordion>
                </div>                   

            </div>
         
        </div>
    )
      
  }


export default Perfil;
