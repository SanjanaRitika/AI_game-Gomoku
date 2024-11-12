/****
 *   GomokuAI class
 *
 *   Basic implementation of the minimax algorithm to determine the optimal move.
 *
 *   Uses a WebWorker to prevent the main UI from freezing.
 */
let calculationCount = 0;

class GomokuAI {
    constructor(gameBoard){
        this.gameBoard = gameBoard;
    }

    findBestMove(){
        return new Promise((resolve, reject) => {

            let matrixState = this.gameBoard.getRawMatrix();
            let offset = null;
            ({matrix: matrixState, off: offset} = Board.reduceMatrix(matrixState, 5));
            const workerInstance = new Worker('worker.js');

            workerInstance.onmessage = event => {
                if(!event.data){
                    reject('Move calculation failed');
                }

                switch(event.data.type){
                    case 'move':
                        let [row, col] = event.data.val;
                        resolve([row + offset.y, col + offset.x]);
                        workerInstance.terminate();
                        break;
                    case 'progress':
                        let completed = event.data.val.completed;
                        let total = event.data.val.total;
                        let progressPercentage = Math.round((completed / total) * 100);
                        document.dispatchEvent(new CustomEvent("progress", {"detail": progressPercentage}));
                        break;
                    case 'log':
                        // Handle logging messages
                        break;
                    case 'debug':
                        // Process debugging events
                        break;
                }
            };

            workerInstance.onError = error => {
                reject(error);
            };

            workerInstance.postMessage({
                matrix: matrixState,
                fn: serializeFunction(Board.evaluateWinner)
            });
        });

        function serializeFunction(fn){
            const functionName = fn.name;
            const functionBody = fn.toString();

            return {
                name: functionName,
                args: functionBody.substring(functionBody.indexOf("(") + 1, functionBody.indexOf(")")),
                body: functionBody.substring(functionBody.indexOf("{") + 1, functionBody.lastIndexOf("}"))
            };
        }
    }
}
