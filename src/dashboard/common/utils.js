function removeNullOrUndefined(object) {

    if (Array.isArray(object)) {
        object.forEach((elem, _index) => {
            if (elem == null || elem == undefined) {
                object.splice(_index,1);
            }
        })
    }
    else if (object instanceof Set || object instanceof Map ) {
        Object.entries(object).forEach((entry) => {
            if (entry[1] == null || entry[1] == undefined) {
                object.delete(entry[0])
            }
        });
    }
    else {
        Array.from(Object.keys(object)).forEach( (prop) => {
            if (object[prop] == null || object[prop] == undefined) {
                delete object[prop]
            }
        })
    }
}


export default {removeNullOrUndefined}