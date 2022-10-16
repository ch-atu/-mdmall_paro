import server from "@/utils/request";

export const api_getPayUrl = (order_id) => {
    return server.request({
        method: 'get',
        url: '/payment/payment/',
        params: {
            order_id
        }
    })
}

export const api_putPayment = (params) => {
    return server.request({
        method: 'put',
        url: '/payment/payment/',
        params
    })
}











