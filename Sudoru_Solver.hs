import Data.List
import Data.Char
import System.IO
import System.Environment
import Data.Function

type Grid = [[Int]]
type Cell = (Int,Int)

--check if grid is complеte
full :: Grid -> Bool
full grid = not (elem 0 (concat grid))

find_all_empty :: Grid -> [(Cell, [Int])]
find_all_empty g = [((r, c), valid_for_cell g (r, c)) |
                    (r, row) <- zip [0..] g, (c, val) <- zip [0..] row, val == 0]

find_minimum:: Grid -> (Cell,[Int])
find_minimum g = minimumBy (\x y -> compare (length $ snd x) (length $ snd y))(find_all_empty g)

valid_row :: [Int] -> Bool
valid_row ls = let sorted = sort ls
                   nums = dropWhile (==0) sorted
                in (length nums == length (nub nums))

valid_for_row :: Grid -> Bool
valid_for_row g = all (valid_row) g 

valid_for_colm :: Grid -> Bool
valid_for_colm g = valid_for_row (transpose g)

valid_for_boxes :: Grid -> Bool
valid_for_boxes g = valid_for_row (box_row g)

row_to_three:: [Int] -> [[Int]] 
row_to_three r = [take 3 r, take 3 (drop 3 r), drop 6 r]

box_row:: Grid -> Grid 
box_row [] = []
box_row (x:y:z:l) = (map concat $ transpose (row_to_three x : row_to_three y : row_to_three z:[])) ++ box_row l

validGrid:: Grid -> Bool
validGrid g = valid_for_colm g && valid_for_boxes g && valid_for_row g


valid_for_cell:: Grid -> Cell -> [Int]
valid_for_cell g (r, c) = let row = g!!r
                              col = (transpose g) !! c
                              box = (box_row g)!!(((r `div` 3) * 3) + (c `div` 3))
                           in [1..9] \\ (row++col++box) 


change_grid:: Grid -> Cell -> Int -> Grid
change_grid  g (r,c) num = let (fstG, (row:sndG)) = splitAt r g
                               (fstR, (_:sndR)) = splitAt c row
                            in fstG++((fstR++(num:sndR)):sndG)

--solve Sudoku
solve' :: [Grid] -> Grid
solve' [] = []
solve' (g:gl) = if validGrid g  == False then solve' gl
                else
                if full g then g
                else let (m, n) = find_minimum g
                      in solve' (map (change_grid g m) n ++ gl)
                {-solve' (map (change_grid g (fst(find_minimum g))) (snd(find_minimum g)) ++ gl)-}

solve :: Grid -> Grid
solve g = solve' [g]  

--Input/Output--
--ignores all strings which are not in grid
gridOnly :: [String] -> [String]
gridOnly s = filter (\x -> length x == 9) s

--from string to grid
makegrid :: [String] -> Grid
makegrid s = map (map digitToInt) s

readAllGrids:: [String] -> [Grid]
readAllGrids [] = []
readAllGrids s = makegrid (fst(splitAt 9 s)) : readAllGrids (snd(splitAt 9 s))

--print grid (from grid to string)
printGrid:: Grid -> String
printGrid g = unlines ((map (\x -> concat $ map show x) g) ++ [" "])

main = do 
      [f] <- getArgs
      content <- readFile f
      let grids = readAllGrids (gridOnly (lines content))
      let solved_grids = map solve grids 
      putStrLn " "
      mapM_ putStr $  map printGrid solved_grids 
