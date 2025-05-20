window.dccFunctions = window.dccFunctions || {};
window.dccFunctions.hideValue = function(value) {
    if (value == -1) {
        return 'All';
    }
    return value
};