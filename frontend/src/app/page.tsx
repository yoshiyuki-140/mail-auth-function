import {
  Center,
  Box,
} from "@yamada-ui/react";


export default function Home() {
  return (
    // 中央に配置されたコンポーネント
    <Center h="100vh" bg="white">
      <Box p='4' bg="blue.500" color="white" borderRadius="md">
        中央に配置されたコンポーネント
      </Box>
    </Center>
  );
}
