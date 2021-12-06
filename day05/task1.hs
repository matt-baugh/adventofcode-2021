import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe

type Board = [[Int]]
type Coord = (Int, Int)
type Line  = (Coord, Coord)


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents


convert :: String -> [Line]
convert xs
  = map convLine $ lines xs

convLine :: String -> Line
convLine s
  = (readCoord c1, readCoord c2)
  where
    [c1, _, c2] = words s
    

readCoord :: String -> Coord
readCoord s
  = (read s1, read s2)
  where
    [s1, s2] = splitOn ',' s


splitOn :: Char -> String -> [String]
splitOn _ "" = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain



solve :: [Line] -> Int
solve ls
  = length $ filter (>= 2) allElems
  where
    ls'        = map orderLine $ filterDiag ls
    finalBoard = foldl updateBoard (genBoard ls) ls'
    allElems   = foldl1 (++) finalBoard


filterDiag :: [Line] -> [Line]
filterDiag ls
  = filter (\((x1, y1), (x2, y2)) -> x1 == x2 || y1 == y2) ls


updateBoard :: Board -> Line -> Board
updateBoard b l
  = rs1 ++ rs2'' ++ rs3
  where
    ((minX, minY), (maxX, maxY)) = l
    (rs1, rs2, rs3)              = splitBetween minY maxY b
    rs2'                         = map (splitBetween minX maxX) rs2
    rs2''                        = map (\(cs1, cs2, cs3) ->
                                        cs1 ++ (map (+1) cs2) ++ cs3) rs2'


splitBetween :: Int -> Int -> [a] -> ([a], [a], [a])
splitBetween i1 i2 xs
  = (first, second, third)
  where
    (first, remaining) = splitAt i1 xs
    (second, third)    = splitAt (i2 - i1 + 1) remaining
    





orderLine :: Line -> Line
orderLine l
  = (minCoord l, maxCoord l)


maxCoord :: Line -> Coord
maxCoord ((x1, y1), (x2, y2))
  = (max x1 x2, max y1 y2)


minCoord :: Line -> Coord
minCoord ((x1, y1), (x2, y2))
  = (min x1 x2, min y1 y2)


genBoard :: [Line] -> Board
genBoard ls
  = replicate (maxY + 1) $ replicate (maxX + 1) 0
  where
    (maxX, maxY) = foldl1 (\c1 c2 -> maxCoord (c1, c2)) $ map maxCoord ls


testInput :: [String]
testInput = [
 "0,9 -> 5,9",
 "8,0 -> 0,8",
 "9,4 -> 3,4",
 "2,2 -> 2,1",
 "7,0 -> 7,4",
 "6,4 -> 2,0",
 "0,9 -> 2,9",
 "3,4 -> 1,4",
 "0,0 -> 8,8",
 "5,5 -> 8,2"]

testData = map convLine testInput
