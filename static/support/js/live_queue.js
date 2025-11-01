function fetchLiveQueue(meetingId){
    // console.log("js", meetingId);
    fetch(`/teacher/live-queue/${meetingId}/`)
    .then(res=>res.json())
    .then(data=>{
        if(data.tickets){ // teacher
            const container=document.getElementById('ticket-list'); container.innerHTML='';
            data.tickets.forEach(t=>{
                const div=document.createElement('div');
                div.className='border p-3 mb-2 rounded flex justify-between items-center bg-gray-50 fade-in';
                div.innerHTML=`<div>
                    <p><strong>#${t.serial_number} - ${t.student}</strong></p>
                    <p>${t.problem_text}</p>
                    <p>Status: ${t.status}</p>
                    ${t.time_left!==null?`<p>Time left: ${t.time_left}s</p>`:''}
                </div>
                <div class="space-x-2">
                    ${t.status==='waiting'?`<button onclick="updateTicket(${t.id},'start')" class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">Start</button>`:''}
                    ${t.status==='joined'?`<button onclick="updateTicket(${t.id},'complete')" class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">Complete</button>`:''}
                </div>`;
                container.appendChild(div);
            });
        } else if(data.ticket){ // student
            const container=document.getElementById('student-ticket'); container.innerHTML='';
            const t=data.ticket;
            const div=document.createElement('div'); div.className='border p-3 rounded bg-gray-50 fade-in';
            div.innerHTML=`<p>Serial: #${t.serial_number}</p>
                <p>Status: ${t.status}</p>
                <p>Position in queue: ${t.position}</p>
                ${t.time_left!==null?`<p>Time left: ${t.time_left}s</p>`:''}`;
            container.appendChild(div);
        }
    });
}

function updateTicket(ticketId, action){
    fetch(`/teacher/update-ticket/`,{
        method:'POST',
        headers:{'X-CSRFToken':getCookie('csrftoken'),'Content-Type':'application/json'},
        body:JSON.stringify({'ticket_id':ticketId,'action':action})
    }).then(res=>res.json()).then(data=>{
        if(data.success) fetchLiveQueue(currentMeetingId);
    });
}

setInterval(()=>{fetchLiveQueue(currentMeetingId);},5000);

function getCookie(name){
    let cookieValue=null;
    if(document.cookie && document.cookie!==''){
        const cookies=document.cookie.split(';');
        for(let i=0;i<cookies.length;i++){
            const cookie=cookies[i].trim();
            if(cookie.substring(0,name.length+1)===(name+'=')){ cookieValue=decodeURIComponent(cookie.substring(name.length+1)); break;}
        }
    }
    return cookieValue;
}
