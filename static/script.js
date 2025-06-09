function approve(requestId) {
    fetch(`/requests/${requestId}/approved`, {
        method: "PUT"
    }).then(() => {
        location.reload();
    });
}

function reject(requestId) {
    fetch(`/requests/${requestId}/rejected`, {
        method: "PUT"
    }).then(() => {
        location.reload();
    });
}