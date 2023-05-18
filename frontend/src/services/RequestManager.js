import React from "react";

const api = axios.create({ baseURL: 'https://cafetorrado-backend.herokuapp.com' });

const authorizeUser = () => {api.get('/authorize')}












export {
    authorizeUser
}