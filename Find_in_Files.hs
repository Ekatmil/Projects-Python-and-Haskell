import System.Directory 
import System.IO
import System.FilePath
import Control.Monad
import Data.List
import System.Environment

allFilesBeneath :: FilePath -> IO [FilePath]
allFilesBeneath dir = do
  subset <- listDirectory dir
  all_files <- forM subset $ \a -> do
    let one_file = combine dir a
    isDir <- doesDirectoryExist one_file
    if isDir 
      then allFilesBeneath one_file
      else return [one_file]
  return (sort (concat all_files))
	
findStr :: String -> String -> Bool
findStr f s = isInfixOf f s

whole_file :: [String] -> String -> [String]
whole_file [] _ = []
whole_file (s:sl) str = if findStr str s == True then s : whole_file sl str else whole_file sl str

findStrInFile :: FilePath -> String -> IO [String]
findStrInFile file str = do
	contents <- readFile file
	let ls = lines contents
	    ls' = whole_file ls str
            f x y = x ++ ": " ++ y
	    result = map (f file)  ls'
        return(result)
	
whole_files_search :: [FilePath] -> String -> IO String
whole_files_search [] _ = return ""
whole_files_search (f:file) str = do
		one_file <- findStrInFile f str
		rest <- whole_files_search file str
		let result = unlines one_file 
		return (result++rest)

run :: [String] -> IO()
run str = if (length str == 2) then
	do
	  ls <- allFilesBeneath (str !! 1)
	  result <- whole_files_search ls (str !! 0)
	  putStr result
	else putStrLn ("usage: find_in_files <string> <dir>")

main = do
    args <- getArgs
    run args 
