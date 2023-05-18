import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Input from '../../components/form/Input';
import SubmitButton from '../../components/form/SubmitButton';
import styles from './CriarGrupo.module.css';
import MultipleSelect from 'react-select';
import Select from '../../components/form/Select';


function CriarPolítica(){

    const [selectedProjectsgitlab, setSelectedProjectsgitlab] = useState([]);
    const [projectsgitlab, setProjectsgitlab] = useState([]);
    const [groupsipa, setGroupsipa] = useState([]);
    const [policy, setPolicy] = useState([]);

    const navigate = useNavigate();

    useEffect(() => {
        const projectsgitlabArray = [];
        fetch('http://localhost:5000/gitlab/project',{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((resp) => resp.json())
            .then((data) => {
                Object.keys(data).map((key) => { 
                    projectsgitlabArray.push(data[key]);

                });
            }).then(setProjectsgitlab(projectsgitlabArray))
            .catch((error)=> console.log(error))
        },[]);

    useEffect(() => {
            const groupsIPAArray = [];
        fetch('http://localhost:5000/ipa/getGroups',{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((resp) => resp.json())
            .then((data) => {console.log(data)
            Object.keys(data).map((key) => groupsIPAArray.push({id: Number(data[key].id), name: data[key].name}));
            }).then(() => { 
            setGroupsipa(groupsIPAArray)})
            .catch((error)=> console.log(error))
    },[]);


    function sendRequestForAddPolicy(policy){
        console.log(policy)
        
        
        fetch('http://localhost:5000/policy', {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(policy),
        })
            .then( (resp) => resp.json())
            .catch((err)  => console.log(err))
            //window.location.replace("http://localhost:3000/politicas");

    }

    
    const submit = (e) => {
        e.preventDefault()
       const newState = {...policy, projectsgitlab: selectedProjectsgitlab};
        setPolicy(newState);
        sendRequestForAddPolicy(newState)
    }

    function handleChange(e){
        setPolicy({ ...policy, policyname: e.target.value})
        console.log(policy, "handlechange")
    }

    function handleGroup(e){
        setPolicy({ ...policy, groupipa: { id: e.target.value, name: e.target.options[e.target.selectedIndex].text}})
    }

    const handleProjects = (item) => {
        setSelectedProjectsgitlab(item);
        console.log("handleproj", projectsgitlab);
       /* setPolicy({ ...policy, projectsgitlab: selectedProjectsgitlab})*/
    }

    
    return (

     
        <div className={styles.form_container}>
            
            <h1>Novo Grupo</h1>
            <p> Formulário para criação de novo grupo de usuários para acesso aos serviços do ambiente do GSI/MPMG</p>

            <form onSubmit={submit} className={styles.form}>    

                <Input type="text" 
                        text="Nome do grupo"
                        name="policyname"
                        placeholder=" Insira o nome do grupo"
                        handleOnChange={handleChange}
                />

                <br></br>
                <h4>Selecione os projetos do Gitlab</h4>
                        
                <MultipleSelect 
                name="projectsgitlab"
                onChange={handleProjects}
                isMulti options={projectsgitlab}
                isClearable={true}
                isSearchable={true}
                isDisabled={false}
                isLoading={false}
                isRtl={false}/>
                
                <br></br>
                <h4>Selecione o grupo do FreeIPA</h4>
                
                <Select name="grupo_id" 
                        options={groupsipa}
                        handleOnChange={handleGroup}
                        
                />
                

            <SubmitButton text="Criar grupo" />
            </form>

        </div>
      
    )
}

export default CriarPolítica;
