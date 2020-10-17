var api_url = "http://localhost:5000";
var app = new Vue({
    el: '#app',
    data: {
        phrase: '',
        loading: false,
        loadingTfIdf: false,
        result: [],
        resultTfIdf: [],
        content: ""
    },
    methods: {        
        findWordInvertIndex: async function (word) {
            const url = api_url + "/find/word/invertindex/" + word;
            try {
                const result = await axios.get(url);
                return result.data.data;
            } catch (error) {
                return [];
            }
        },

        findWordTfIdf: async function (word) {
            const url = api_url + "/find/word/tfidf/" + word;
            try {
                const result = await axios.get(url);
                return result.data.data;
            } catch (error) {
                return [];
            }
        },

        getDataOfText: async function (key) {
            console.log("getDataOfText", key);
            const url = api_url + "/find/file/" + key;
            try {
                const result = await axios.get(url);
                this.content = result.data.text || "";
                $("#content-modal").modal("show");
            } catch (error) {
                console.log("error", error);
            }
        },

        getJsonOfText: function (key) {
            window.open(api_url + "/find/file/" + key, '_blank');
        },

        operateInput: async function () {
            let str = this.phrase;
            let inputList = str.split(/\b\s+/);
            this.operateWithInvertedIndex(inputList);
            this.operateWithTfIdf(inputList);
        },
        async operateWithInvertedIndex(inputList){
            let result = [];
            let operation = null;
            this.loading = true;
            for (let word of inputList) {
                if(["and","or","not"].includes(word)){
                    operation = word;
                }
                else{
                    const query = await this.findWordInvertIndex(word) || [];
                    result = operateList(result,query, operation);
                    operation = null;
                }
            }
            this.loading = false;
            this.result = sortByValue(result);
        },

        async operateWithTfIdf(inputList){
            let result = [];
            let operation = null;
            this.loadingTfIdf = true;
            for (let word of inputList) {
                if(["and","or","not"].includes(word)){
                    operation = word;
                }
                else{
                    const query = await this.findWordTfIdf(word) || [];
                    result = operateList(result,query, operation);
                    operation = null;
                }
            }
            this.loadingTfIdf = false;
            this.resultTfIdf = sortByValue(result);
        }

    },
    mounted() {

    }
})


function operateList(list1, list2, op="or"){
    if(op==="and"){
        console.log("and");
        return andOperation(list1,list2);
    }
    else if(op==="not"){
        console.log("not");
        return notOperation(list1,list2);
    }
    else if (op==="or"){
        console.log("or");
        return orOperation(list1,list2);
    }
    return orOperation(list1,list2);
}

// L1 interseccion L2 
function andOperation(list1,list2){
    let result = [];
    for(let item of list1){
        const index = list2.findIndex(item2 => item2.docId === item.docId);
        if(index>=0){
            item.value += list2[index].value;
            result.push(item);
        }
    }
    return result;
}

// L1 union L2
function orOperation(list1, list2){
    let result = [];
    for(let item of list1){
        const index = list2.findIndex(item2 => item2.docId === item.docId);
        if(index>=0){
            item.value += list2[index].value;
        }
        result.push(item);
    }

    for(let item of list2){
        const index = result.findIndex(item2 => item2.docId === item.docId);
        if(index===-1){
            result.push(item);
        }
    }

    return result;


}

// L1 not L2
function notOperation(list1, list2){
    let result = [];
    for(let item of list1){
        const index = list2.findIndex(item2 => item2.docId === item.docId);
        if(index===-1){
            result.push(item);
        }
    }
    return result;
}


function sortByValue (result){
    return result.sort((a, b) => {
        if (a.value > b.value) {
            return -1
        }
        if (a.value < b.value) {
            return 1
        }
        return 0;
    })
}