const SIZE = 10;

class Board {
    constructor(parentNode, onSquareClickedCb) {
        this.matrix = [];
        this.parentNode = parentNode;

        // generate board
        for (let i = 0; i < SIZE; i++) {
            let r = [];
            let row = document.createElement("div");
            row.classList.add('row');
            row.classList.add(i);

            for (let j = 0; j < SIZE; j++) {
                let square = new Square(i, j);
                square.setOnClick(onSquareClickedCb(i, j));
                row.appendChild(square.getDomObj());
                r.push(square);
            }

            parentNode.appendChild(row);
            this.matrix.push(r);
        }
    }

    getSize() {
        return SIZE;
    }

    getOccupiedSquares() {
        return this.matrix.reduce((arr, row) => {
            arr.push(...row.filter(square => square.isOccupied()));
            return arr;
        }, []);
    }

    getSquare(row, col) {
        try {
            return this.matrix[row][col];
        } catch (e) {
            console.log(e);
        }
    }

    getMatrix() {
        return this.matrix;
    }

    getRawMatrix() {
        return this.matrix.reduce((arr, row) => {
            row = row.reduce((a, c) => {
                a.push(c.getVal());
                return a;
            }, []);
            arr.push(row);
            return arr;
        }, []);
    }

    getRow(num) {
        return this.matrix[num];
    }

    static pruneMatrix(matrix, padding) {
        let left = Infinity, right = 0, top = Infinity, bottom = 0;
        const MATRIX_SIZE = 10;

        for (let i = 0; i < matrix.length; i++) {
            for (let j = 0; j < matrix[i].length; j++) {
                if (matrix[i][j]) {
                    top = Math.min(top, i);
                    bottom = Math.max(bottom, i);
                    left = Math.min(left, j);
                    right = Math.max(right, j);
                }
            }
        }

        if (padding) {
            left = Math.max(0, left - padding);
            right = Math.min(MATRIX_SIZE, right + padding);
            top = Math.max(0, top - padding);
            bottom = Math.min(MATRIX_SIZE, bottom + padding);
        }

        if ((right - left) - (bottom - top)) {
            console.log('normalizing pruned size');
            console.log('left: %s, right: %s, top: %s, bottom: %s', left, right, top, bottom);

            let width = right - left;
            let height = bottom - top;
            let size = Math.max(width, height);

            if (width !== size) {
                let x = size - width;
                left = Math.max(0, left - Math.floor(x / 2));
                right = Math.min(9, right + Math.floor(x / 2));
                x = size - (right - left);

                if (x) {
                    if (left) {
                        left -= x;
                    } else {
                        right += x;
                    }
                }
            } else if (height !== size) {
                let x = size - height;
                top = Math.max(0, top - Math.floor(x / 2));
                bottom = Math.min(9, bottom + Math.floor(x / 2));
                x = size - (bottom - top);

                if (x) {
                    if (top) {
                        top -= x;
                    } else {
                        bottom += x;
                    }
                }
            }

            if ((bottom - top) !== (right - left)) {
                console.log('error!! unequal sizes!!!');
            }
        }

        let copy = [];

        for (let i = top; i <= bottom; i++) {
            let row = [];
            for (let j = left; j <= right; j++) {
                row.push(matrix[i][j]);
            }
            copy.push(row);
        }

        return {
            'matrix': copy,
            'off': {
                'x': left,
                'y': top
            }
        };
    }

    static checkWinner3(matrix, hMask1, hMask2, vMask, dMask1, dMask2) {
        matrix = [].concat.apply([], [...matrix]);

        for (let i = 0; i < matrix.length; i++) {
            if (matchMask(matrix, hMask1, i)) return 1;
            if (matchMask(matrix, hMask2, i)) return 1;
            if (matchMask(matrix, vMask, i)) return 1;
            if (matchMask(matrix, dMask1, i)) return 1;
            if (matchMask(matrix, dMask2, i)) return 1;
        }

        return 0;

        function matchMask(matrix, mask, start) {
            if (matrix.length < mask.length + start) {
                return false;
            }
            for (let i = 0; i < mask.length; i++) {
                if (mask[i] && !matrix[start + i]) return false;
            }
            return true;
        }
    }

    static checkWinner2(matrix) {
        const IN_A_ROW = 5;
        for (let i = 0; i < matrix.length - IN_A_ROW; i++) {
            for (let j = 0; j < matrix[i].length; j++) {
                let resH = 1, resV = 1, resD1 = 1, resD2 = 1;

                for (let k = 0; k < IN_A_ROW; k++) {
                    resH &= matrix[j][i + 1 + k];
                    resV &= matrix[i + 1 + k][j];
                    resD1 &= matrix[i + k][j + k];
                    resD2 &= matrix[i + k][j + 4 - k];
                }

                if (resH || resV || resD1 || resD2) return 1;
            }
        }
        return 0;
    }

    static checkWinner(matrix) {
        for (let i = 0; i < matrix.length; i++) {
            let res = { hor: {}, ver: {}, dg1: {}, dg2: {}, dg3: {}, dg4: {} };

            for (let key in res) {
                res[key] = { streak: 0, current: 0 };
            }

            for (let j = 0; j < matrix[i].length; j++) {
                let winner = check(matrix[i][j], res.hor);
                if (winner) return winner;

                winner = check(matrix[j][i], res.ver);
                if (winner) return winner;

                if (i < 4 || j > i) continue;

                let len = matrix.length;
                winner = check(matrix[i - j][j], res.dg1);
                if (winner) return winner;

                winner = check(matrix[len - 1 - j][i - j], res.dg2);
                if (winner) return winner;

                winner = check(matrix[j][len - 1 - i + j], res.dg3);
                if (winner) return winner;

                winner = check(matrix[len - 1 - i + j][len - 1 - j], res.dg4);
                if (winner) return winner;
            }
        }
        return 0;

        function check(square, obj) {
            if (square) {
                if (square === obj.current) {
                    obj.streak++;
                } else {
                    obj.streak = 1;
                    obj.current = square;
                }
            } else {
                obj.streak = 0;
                obj.current = 0;
            }
            return obj.streak === 5 ? obj.current : 0;
        }
    }

    showAnimation() {
        return new Promise(async (resolve, reject) => {
            let boardSize = board.getSize();
            let squareList = Array.from({ length: boardSize * boardSize }, (k, v) => v);
            squareList.sort(() => Math.random() - 0.5);

            for (let i = 0; i < squareList.length; i += 10) {
                let promises = Array.from({ length: 10 }, (k, v) => v);
                promises = promises.map(a => {
                    let num = squareList[i + a];
                    let x = num % boardSize, y = Math.floor(num / boardSize);
                    return board.getSquare(y, x).twinkle();
                });
                await Promise.all(promises);
            }

            squareList.sort(() => Math.random() - 0.5);

            for (let i = squareList.length - 1; i > 0; i -= 10) {
                let promises = Array.from({ length: 10 }, (k, v) => v);
                promises = promises.map(a => {
                    let num = squareList[i - a];
                    let x = num % boardSize, y = Math.floor(num / boardSize);
                    return board.getSquare(y, x).untwinkle();
                });
                await Promise.all(promises);
            }

            resolve();
        });
    }

    delete() {
        this.parentNode.innerHTML = '';
    }
}
