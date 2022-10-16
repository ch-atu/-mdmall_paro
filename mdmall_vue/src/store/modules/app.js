export default {
    namespaced: true,
    state: {
        active_data:'',
        kw:''
    },
    actions: {},
    mutations: {
        CHANGE_ACTIVE(state, value){
            state.active_data = value
        },
        CHANGE_KW(state, value){
            state.kw = value
        }
    },
    getters: {},
}
