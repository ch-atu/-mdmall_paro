import server from "@/utils/request";

export const register = (data) => {
    return server.request({
        method:'post',
        url:'/user/users/',
        data
    })
}

export const checkUser = (username) => {
    return server.request({
        method:'get',
        url:`/user/usernames/${username}/count/`
    })
}

export const checkTel = (mobile) => {
    return server.request({
        method:'get',
        url:`/user/mobiles/${mobile}/count/`
    })
}

export const login = (data) => {
    return server.request({
        method:'post',
        url:`/user/authorizations/`,
        data
    })
}

export const getUser = () => {
    return server.request({
        method:'get',
        url:'/user/user/',
    })
}

export const changePass = (data, user_id) => {
    return server.request({
        method:'put',
        url:`/user/change_pass/${user_id}/`,
        data
    })
}

export const getHome = () =>{
    return server.request({
        method:'get',
        url:'/user/user_homes/'
    })
}

export const addHome = (data) =>{
    return server.request({
        method:'post',
        url:'/user/user_homes/',
        data
    })
}

export const editHome = (data, home_id) => {
    return server.request({
        method:'put',
        url:`/user/user_home/${home_id}/`,
        data
    })
}

export const deleteHome = (home_id) =>{
    return server.request({
        method:'delete',
        url:`/user/user_home/${home_id}/`,
    })
}

export const api_checkEmail = (email)=>{
    return server.request({
        method:'get',
        url:`/user/email/${email}/count/`,
        params:{
            email
        }
    })
}

export const addEmail = (data) => {
    return server.request({
        method:'post',
        url:'/user/email/',
        data
    })
}

export const activeEmail = () => {
    return server.request({
        method:'put',
        url:'/user/email/',
    })
}

export const checkActiveEmail = (token) => {
    return server.request({
        method:'get',
        url:'/user/email/',
        params:{
            token
        }
    })
}

export const addHistory = (data)=>{
    return server.request({
        method:'post',
        url:'/user/history/',
        data
    })
}

export const getHistory = ()=>{
    return server.request({
        method:'get',
        url:'/user/history/',
    })
}


