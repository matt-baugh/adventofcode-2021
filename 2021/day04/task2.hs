import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe

type Board = [[Int]]
type Mask = [[Bool]]
type Player = (Board, Mask)

realResult = do
        allContents <- readFile "data.txt"
        let (xs, bs) = convert allContents
        return $ solve xs bs


convert :: String -> ([Int], [Board])
convert xs
  = (getNums ys, groupBoards bis)
  where
    ys : bss = filter (/= "") $ lines xs
    bis = map ((map read) . words) bss


getNums :: String -> [Int]
getNums xs
  = map read $ splitOn ',' xs

splitOn :: Char -> String -> [String]
splitOn _ "" = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain



groupBoards :: [[Int]] -> [Board]
groupBoards [] = []
groupBoards bs = xs : groupBoards ys
  where
    (xs, ys) = splitAt 5 bs


boardToPlayer :: Board -> Player
boardToPlayer b
  = (b, replicate 5 $ replicate 5 False)



solve :: [Int] -> [Board] -> Int
solve xs bs
  = solve' xs $ map boardToPlayer bs


solve' :: [Int] -> [Player] -> Int
solve' (x : xs) ps
  | wins == [True] = x * sumScore
  | otherwise      = solve' xs ps''
  where
    ps'        = updatePlayers x ps
    wins       = checkWin ps'
    lIs        = elemIndices False wins
    ps''       = map (ps' !!) lIs
    [(lB, lM)] = ps'
    sumScore = sum $ map sumNegate $ zip lB lM
    sumNegate :: ([Int], [Bool]) -> Int
    sumNegate (ys, bs)
      = foldl (\acc (y, b) -> acc + (y * (fromEnum $ not b))) 0 $ zip ys bs

updatePlayers :: Int -> [Player] -> [Player]
updatePlayers x ps
  = map uP ps
  where
    uP :: Player -> Player
    uP (b, m)
      | isNothing rIm = (b, m)
      | otherwise    = (b, frs ++ [fcs ++ [True] ++ lcs] ++ lrs)
      where
        cIs             = map (elemIndex x) b
        rIm             = findIndex isJust cIs
        rI              = fromJust rIm
        cI              = fromJust $ cIs !! rI
        (frs, (cr:lrs)) = splitAt rI m
        (fcs, (_ :lcs)) = splitAt cI cr


checkWin :: [Player] -> [Bool]
checkWin ps
  = map (cw' . snd) ps
  where
    cw' :: Mask -> Bool
    cw' m
      = winRow || winCol
      where
        winRow = isJust $ elemIndex True $ map (foldl1 (&&)) m
        winCol = isJust $ elemIndex True $ map (foldl1 (&&)) $ transpose m


testNumbers :: [Int]
testNumbers = [7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1]

testBoards :: [Board]
testBoards =groupBoards $ map ((map read) . words) ["22 13 17 11  0",
 "8  2 23  4 24",
 "21  9 14 16  7",
 "6 10  3 18  5",
 "1 12 20 15 19",

 "3 15  0  2 22",
 "9 18 13 17  5",
 "19  8  7 25 23",
 "20 11 10 24  4",
 "14 21 16 12  6",

 "14 21 17 24  4",
 "10 16 15  9 19",
 "18  8 23 26 20",
 "22 11 13  6  5",
 "2  0 12  3  7"]

p1 :: Player
p1 = ([[1, 3], [2, 4]], [[False, False], [False, False]])    
