const feedbackToast = document.createElement("div");
feedbackToast.style.position = "fixed";
feedbackToast.style.bottom = "20px";
feedbackToast.style.right = "20px";
feedbackToast.style.padding = "10px 20px";
feedbackToast.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
feedbackToast.style.color = "#ffffff";
feedbackToast.style.borderRadius = "8px";
feedbackToast.style.fontFamily = "sans-serif";
feedbackToast.style.fontSize = "14px";
feedbackToast.style.zIndex = "999999";
feedbackToast.style.opacity = "0";
feedbackToast.style.transform = "translateY(20px)";
feedbackToast.style.transition = "opacity 0.3s ease, transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
feedbackToast.style.pointerEvents = "none";
document.body.appendChild(feedbackToast);

let feedbackTimeout;

const friendlyNames = {
    "left_click": "Left Click 🖱️",
    "right_click": "Right Click 🖱️",
    "double_click": "Double Click 🖱️",
    "scroll": "Scrolling ↕️",
    "drag": "Dragging ✋",
    "release_drag": "Drop 🤚"
};

const ignoredActions = ["move", "holding_click", "left_click_intent"];

setInterval(() => {
    chrome.runtime.sendMessage({ action: "get_state" }, (response) => {
        if (response && !ignoredActions.includes(response.action)) {
            console.log("Ação detectada pelo WGI:", response.action);
            
            const actionText = friendlyNames[response.action] || response.action;
            feedbackToast.innerText = `Gesture: ${actionText}`;
            feedbackToast.style.opacity = "1";
            feedbackToast.style.transform = "translateY(0)";
            
            // Hide it again after 1 second
            clearTimeout(feedbackTimeout);
            feedbackTimeout = setTimeout(() => {
                feedbackToast.style.opacity = "0";
                feedbackToast.style.transform = "translateY(20px)";
            }, 1000);
        }
    });
}, 50);