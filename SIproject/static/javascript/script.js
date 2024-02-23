const likeSession = [];
const unlikeSession = [];
let objID;
let likes;


function ifAlreadyLiked(objID) {
    if (likedList.includes(objID)) {
        document.getElementById("Lpost"+objID).innerHTML = "Unlike Post";
        document.getElementById("Lpost"+objID).classList.remove('btn-outline-success');
        document.getElementById("Lpost"+objID).classList.add('btn-success');
    }
} 

function Add(id, likes)
{
    if (document.getElementById("Lpost"+id).innerHTML == "Unlike Post") {
        document.getElementById("Lpost"+id).innerHTML = "Like Post";
        document.getElementById('Lpost'+id).classList.remove('btn-success');
        document.getElementById('Lpost'+id).classList.add('btn-outline-success');
        
        unlikeSession.push(id);
        document.getElementById('unlikeProcess').value = unlikeSession.join("-");
        document.getElementById('unlikeProcess2').value = unlikeSession.join("-");
        document.getElementById('unlikeProcess3').value = unlikeSession.join("-");
        if (likeSession.includes(id)) {
            likeSession.splice(unlikeSession.indexOf(id), 1);
        }
        document.getElementById("Likes"+id).innerHTML = "Likes = " + (parseInt(document.getElementById("Likes"+id).innerHTML.match(/\d+(\.\d+)?/g))-1).toString();


    }
    else if (document.getElementById("Lpost"+id).innerHTML == "Like Post") {
        document.getElementById("Lpost"+id).innerHTML = "Unlike Post";
        document.getElementById('Lpost'+id).classList.remove('btn-outline-success');
        document.getElementById('Lpost'+id).classList.add('btn-success');
        likeSession.push(id);
        document.getElementById('likeProcess').value = likeSession.join("-");
        document.getElementById('likeProcess2').value = likeSession.join("-");
        document.getElementById('likeProcess3').value = likeSession.join("-");
        if (unlikeSession.includes(id)) {
            unlikeSession.splice(unlikeSession.indexOf(id), 1);
        }
        document.getElementById("Likes"+id).innerHTML = "Likes = " + (parseInt(document.getElementById("Likes"+id).innerHTML.match(/\d+(\.\d+)?/g))+1).toString();;
    }
    
    
    
}

function getPost(x) {
    document.getElementById("selectedPost").value = x
}

function getPostR(x) {
    document.getElementById("reportedPost").value = x
    document.getElementById("mainForm").action = "afterPostReport";
}

function updateSearchButtons() {
    currentSearch = document.querySelector(".searcher").value;
    document.getElementById("searchPost").innerHTML = `search for '${currentSearch}' in Posts'`;
    document.getElementById("searchUser").innerHTML = `search for '${currentSearch}' in Users'`;
    document.getElementById('searchPost').classList.remove('d-none');
    document.getElementById('searchUser').classList.remove('d-none');

    if (currentSearch.length == 0) {
        document.getElementById('searchPost').classList.add('d-none');
        document.getElementById('searchUser').classList.add('d-none');

    }

}

function postOrUser(x) {
    document.getElementById('userOrPost').value = x;
    console.log("pls be fixed")
    console.log(document.getElementById('userOrPost').value);

}

function getPostD(x) {
    document.getElementById("delpost").value = x
    document.getElementById("mainForm").action = "profile";
}




