import axios from "axios";


const BASE_URL = import.meta.env.PROD

    ? "https://querydocs-backend.onrender.com"

    : "http://127.0.0.1:8000";



const API = axios.create({

    baseURL: BASE_URL

});



export default API;