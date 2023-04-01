import styles from './GrupoPoliticas.module.css'
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

function GrupoPoliticas(){

    const navigate = useNavigate();

    const [grupoDePoliticas, setgrupoDePoliticas] = useState([])

    useEffect(() => {
        
        fetch('http://localhost:5000/policy',{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((resp) => resp.json())
            .then((data) => {
              console.log(data)
              setgrupoDePoliticas(data)
            })
            .catch((error)=> console.log(error))

    }, [])


    return (
       
        <div className={styles.grupoPoliticas_container}>
            
            

            <Button sx={{position: 'absolute', right: '11%'}} component={Link} to={'/criargrupo'} variant="contained" startIcon={<AddIcon />}>
                Criar novo grupo de politica
            </Button>
            <br></br>
            <br></br>
            <br></br>
                        
            <h1>Grupo de Políticas</h1>
            


            <div >
                {grupoDePoliticas.map((gp) => (
                
                <div key={gp.policyid}>
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
                             <Typography sx={{ fontWeight: 'bold', fontSize: 16 }}>{gp.name}</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <Typography>
                                Projetos GitLab:
                                {Object.keys(gp.projectsgitlab).map((item) => 
                                    <li key={item}>{item}</li>
                                )}
                            </Typography>

                            <Typography>
                                <br></br>
                                Grupo FreeIpa: <li>{gp.groupipa}</li>
                            </Typography>
                                    <br></br>

                            <Button component={Link} to={`/politica/${gp.policyid}`} variant="outlined" startIcon={<ReadMoreIcon />}>
                                Detalhes
                            </Button>
                        </AccordionDetails>
 
                    </Accordion>
                </div>                   
                ))}

            </div>
         
        </div>
    )
      
  }


export default GrupoPoliticas;
