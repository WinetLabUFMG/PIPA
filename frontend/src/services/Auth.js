import Cookies from 'js-cookies';

const isAuthenticated = () => Cookies.getItem("access_token_cookie") !== null;

export { isAuthenticated}