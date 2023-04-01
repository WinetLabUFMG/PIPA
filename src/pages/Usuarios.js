import styles from './Usuarios.module.css'
import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';


import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ReadMoreIcon from '@mui/icons-material/ReadMore';
import Button from '@mui/material/Button';


function Usuarios(){

    const [usuarios, setUsuarios] = useState([])

    useEffect(() => {
        
        fetch('http://localhost:5000/user',{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((resp) => resp.json())
            .then((data) => {
              console.log(data)
                setUsuarios(data)
            })
            .catch((error)=> console.log(error))

    }, [])
    

    return (

        <div className={styles.usuarios_container}>
          <h1> Usuários </h1>
          
          
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 'bold', fontSize: 16 }} >Nome</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', fontSize: 16 }} align="center">Email</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', fontSize: 16 }} align="center">Username&nbsp;</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', fontSize: 16 }} align="center">Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {usuarios.map((row) => (
                  
                  <TableRow
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      {row.fullname}
                    </TableCell>
                    <TableCell align="center">{row.email}</TableCell>
                    <TableCell align="center">{row.username}</TableCell>
                    <TableCell align="center">

                      <Button component={Link} to={`/usuario/${row.username}`} variant="outlined" startIcon={<ReadMoreIcon />}>
                          Editar
                      </Button>
                      &ensp;      
                      <Button component={Link} to={`/usuario/${row.username}`} variant="outlined" startIcon={<CheckCircleOutlineIcon />} disabled>
                          Validar
                      </Button>
                      &ensp;

                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      );



}



export default Usuarios;