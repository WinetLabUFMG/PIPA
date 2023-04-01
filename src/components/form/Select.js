import styles from './Select.module.css'

function Select({ text, name, options, handleOnChange, value}){
console.log(options);
    return(
        <div className={styles.form_control}>
            <label htmlFor={name}>{text}</label>
            <select name={name} id={name} onChange={handleOnChange} >
                <option>Selecione um grupo</option>
               {options.map((option) =>(
                <option value={`${option.id}`} key={option.id}>
                    {option.name}
                </option>
               ))}
            </select>
        </div>
    )

}

export default Select