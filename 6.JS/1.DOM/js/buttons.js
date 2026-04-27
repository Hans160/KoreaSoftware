
        //각자의 버튼이 눌릴때마다 위에 div의 숫자가 1씩 증가하거나 감소하도록 만들어보자
        const zero = document.getElementById('zero');

        function plus() {
            zero.textContent = parseInt(zero.textContent) + 1;
        }

        function minus() {
            zero.textContent = parseInt(zero.textContent) - 1;
        }

        const button1 = document.getElementById('incButton');
        const button2 = document.getElementById('decButton');

        /* 이벤트 핸들러 */
        button1.addEventListener('click',()=> {
            zero.textContent = parseInt(zero.textContent) + 1;
        });
        button2.addEventListener('click',()=> {
            zero.textContent = parseInt(zero.textContent) - 1;
        });