import server from "@/utils/request";


export const getMobiles = () => {
    return server.request({
        method: 'get',
        url: '/goods/mobiles/'
    })
}



export const getComputers = () =>  {
    return server.request({
        method:'get',
        url:'/goods/computers/'
    })
}

export const getGoodDetail = (pk, category) =>{
    return server.request({
        method:'get',
        url:`goods/detail/${pk}/?category=${category}`
    })
}

export const api_goodsSearch = (name, page=1)=>{
    return server.request({
        method:'get',
        url:'/goods/api/search/',
        params:{
            'name__icontains':name,
            page
        }
    })
}














