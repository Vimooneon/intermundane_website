function showTable(){
    const val = document.getElementById("panel-select").value;
    if (val=="latest-logs"){
        document.getElementById("latest-logs").style.display = "block";
        document.getElementById("user-manage").style.display = "none";
    }else if (val=="user-manage"){
        document.getElementById("latest-logs").style.display = "none";
        document.getElementById("user-manage").style.display = "block";
    }
}
function showActions(username){
    if (document.getElementById("user_actions_"+username).style.display == "none"){
        document.getElementById("user_actions_"+username).style.display = "block";
    }else{
        document.getElementById("user_actions_"+username).style.display = "none";
    }
}

function filterLogs() {
    const usernameFilter = document.getElementById("name_filter").value.trim().toLowerCase();
    const sourceFilter = document.getElementById("source_filter").value.trim().toLowerCase();
    const actionFilter = document.getElementById("action_filter").value.trim().toLowerCase();
    const timestampFilter = document.getElementById("timestamp_filter").value.trim().toLowerCase();

    const rows = document.querySelectorAll("#latest-logs-table tbody tr");

    rows.forEach((row) => {

        const username = row.querySelector(".username").textContent.trim().toLowerCase();

        const source = row.querySelector(".source").textContent.trim().toLowerCase();

        const action = row.querySelector(".action").textContent.trim().toLowerCase();

        const timestamp = row.querySelector(".timestamp").textContent.trim().toLowerCase();

        const usernameMatch = username.includes(usernameFilter);

        const sourceMatch = sourceFilter === "" || source === sourceFilter;

        const actionMatch = action.includes(actionFilter);

        const timestampMatch = timestamp.includes(timestampFilter);

        if (usernameMatch && sourceMatch && actionMatch && timestampMatch) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

