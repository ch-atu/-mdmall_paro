export default {
    namespaced: true,
    state: {
        count:0
    },
    actions: {},
    mutations: {
        RESETCOUNT(state, value){
            state.count = value
        },
        CLEAR(state, value){
            // console.log(state);
            for (let i in state){
                state[i] = ''
            }
        },
    },
    getters: {},
}
