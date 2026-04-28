        let interval;
        let timerId;
        const timeInput = document.getElementById('timeInput');
        const progress = document.getElementById('progress');
        const progressText = document.getElementById('progressText');
        const startButton = document.getElementById('startButton');
        const clearButton = document.getElementById('clearButton');

        startButton.addEventListener('click', startProgress);
        clearButton.addEventListener('click', clearProgress);

        function startProgress() {
            duration = parseInt(timeInput.value);
            console.log('입력초', duration);

            let elapsed =0; //초과 시간
            
            timerId = setInterval(() => {
                // console.log('반복호출')
                elapsed++;
                const ratio = Math.floor((elapsed / duration) * 100); // 진행율 계산
                progress.style.width = `${ratio}%`;
                progressText.textContent = `${ratio}%`;
                console.log(progress);
                console.log(ratio);

                if (ratio >= 100) {
                    //타이머 중지
                    clearInterval(timerId)
                    console.log("끝났습니다");
                    startButton.disabled= false;
                }
            }, 1000);
        }

        function clearProgress() {
            progress.style.width = '2px';  // 살짝 보이게...
            timeInput.value="";
            progressText.textContent = '0%';
        }
       