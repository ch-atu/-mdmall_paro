import server from "@/utils/request";

export const api_addOrderTemp = (data) => {
    return server.request({
        method: 'post',
        url: '/order/order_temp/',
        data
    })
}


export const api_getOrderTemp = () => {
    return server.request({
        method: 'get',
        url: '/order/order_temp/',
    })
}


export const api_addOrderForever = (data) => {
    return server.request({
        method:'post',
        url:'/order/order_forever/',
        data
    })
}


export const api_getOrderForever = (page) => {
    return server.request({
        method:'get',
        url:'/order/order_forever/',
        params:{
            page,
        }
    })
}

export const api_getOrderLatest = () => {
    return server.request({
        method:'get',
        url:'/order/order_latest/',
    })
}





















