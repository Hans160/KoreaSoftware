document.addEventListener('DOMContentLoaded', () => {
    const res =await fetch('/list');
    const data = await res.json();
    console.log(data);
    const result = document.getElementById('card-list');

    data.forEach(post => {
        
    });
});
function makeCard(id,title, message) {
    const card = document.createElement('div');
    card.innerHTML = `
    <div>
        <div class="card-body">
            <p>${id}</p>
            <p>${title}</p>
            <p>${message}</p>
            <button>수정</button>
            <button>삭제</button>
        </div>
    </div>
    `;
    document.getElementById('card-list').appendChild(card);   
}

document.getElementById('input-submit').addEventListener('click', () => {
    const title = document.getElementById('input-title').value;
    const message = document.getElementById('input-text').value;

    fetch('/creat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'},
        body: JSON.stringify({title: title, message: message})
    })
        
        
        
    });

