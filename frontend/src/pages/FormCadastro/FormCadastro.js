import {useState , useEffect} from 'react'
import { useNavigate } from 'react-router-dom'


import Input from '../../components/form/Input';
import SubmitButton from '../../components/form/SubmitButton';
import styles from './FormCadastro.module.css'


function FormularioCadastro(){
    
     const history = useNavigate()

    const [user, SetUser] = useState()
    const [groupsipa, setGroupsipa] = useState([]);

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

    function sendRequestForAddUser(user){
        
        console.log(user)
        
        
        fetch('http://localhost:5000/user', {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(user),
        })
            .then( (resp) => resp.json())
            .then( (data) => { 
                console.log(data)
                history('/cadastro', { message: 'Solicitação enviada com sucesso!' })
            })
            .catch((err)  => console.log(err))
        
    }

    
    const submit = (e) => {
        e.preventDefault()
        sendRequestForAddUser(user)
    }
   

   
    function handleChange(e){
        SetUser({ ...user, [e.target.name]: e.target.value})
        console.log(user)
    }

    
    
    return (

     
        <div className={styles.form_container}>
            
            <h1>Solicitação de acesso</h1>
            <p> Formulário para solicitar criação de usuário para acesso ao ambiente do GSI/MPMG</p>

            <form onSubmit={submit} className={styles.form}>    

                <Input type="text" 
                        text="Primeiro nome"
                        name="firstName"
                        placeholder=" Insira seu primeiro nome"
                        handleOnChange={handleChange}
                />

                <Input type="text" 
                        text="Sobrenome"
                        name="lastName"
                        placeholder="Insira seu sobrenome"
                        handleOnChange={handleChange}
                />

                <Input type="text" 
                        text="Email"
                        name="email"
                        placeholder="Insira seu email"
                        handleOnChange={handleChange}
                />

                <Input type="text" 
                        text="Username"
                        name="username"
                        placeholder="Insira um username"
                        handleOnChange={handleChange}
                />


                <SubmitButton route="/usuarios" text="Enviar solicitação" />
            </form>

        </div>
      
    )
}

export default FormularioCadastro;
