import server from "@/utils/request";

export const api_addCart = (data)=>{
    return server.request({
        method:'post',
        url:'/cart/carts/',
        data
    })
}

export const api_getCart = ()=>{
    return server.request({
        method:'get',
        url:'/cart/carts/',
    })
}

export const api_updateCart = (data)=>{
    return server.request({
        method:'put',
        url:'/cart/api/',
        data
    })
}

export const api_deleteCart = (data)=>{
    return server.request({
        method:'delete',
        url:'/cart/api/',
        data
    })
}

export const api_getCartCount = ()=>{
    return server.request({
        method:'get',
        url:'/cart/carts/count/'
    })
}











