import axios from "axios";
import { getCookie } from "../cookies/cookies";
import { PROD_BASE_URL } from "../main";

async function auth({to, next}){
    const id = getCookie("id");
    const name = getCookie("name");
    const email = getCookie("email");
    const isFirstAccess = id == "" ||  name == "" || email == "";

    if(isFirstAccess){
        return next({
            name: 'auth', 
            query: {redirect: "/"}
        })
    }
    
    try {
        const userData = await axios.get(`${PROD_BASE_URL}/user/${id}`)
        const isRedirectToKitchen = to.fullPath.includes("kitchen");
        const isRedirectToManager = to.fullPath.includes("manager");
        const isRedirectToCashier = to.fullPath.includes("cashier")
        
        const isCustomer = userData.data.user_type == 0;
        const isChief = userData.data.user_type == 1;
        const isCashier = userData.data.user_type == 2
        const isManager = userData.data.user_type == 3;
        const isAdmin = userData.data.user_type == 4;

        const isValidUser = (userData.data.email == email && userData.data.name == name && userData.data.id == id)
        const isValidRedirect = (isManager) || (isAdmin) || (isRedirectToKitchen && (isChief)) || (isRedirectToCashier && (isCashier));

        if(!isValidUser || !isValidRedirect){
            alert("No access rights");
            return next({
                name: 'auth', 
                query: {redirect: "/"}
            });
       }
    return next();
        
    } catch (error) {
        alert("Error logging in");
        return next({
            name: 'auth', 
            query: {redirect: "/"}
        })
    }


 
}

function authPipeline (context, middleware, index) {
    const nextMiddleware = middleware[index]
 
    if(!nextMiddleware){
        return context.next
    }
 
    return () => {
        const nextPipeline = authPipeline(
            context, middleware, index + 1
        )
 
        nextMiddleware({ ...context, next: nextPipeline })
 
    }
 }

 export {auth, authPipeline}