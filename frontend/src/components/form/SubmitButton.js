import styles from './SubmitButton.module.css'
import { useNavigate } from 'react-router-dom'

function SubmitButton({ text , route}){
    const navigate = useNavigate();

    return(
        <div>
            <button className={styles.btn}>{text}</button>
        </div>
    )

}

export default SubmitButton