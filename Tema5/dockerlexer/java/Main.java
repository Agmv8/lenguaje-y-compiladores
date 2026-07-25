package dockerlexer;

import java.nio.file.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.err.println("Uso: java dockerlexer.Main <archivo.dockerfile>");
            System.exit(1);
        }

        String content = Files.readString(Paths.get(args[0]));
        List<Parser.Node> ast = Parser.parseDockerfile(content);

        StringBuilder sb = new StringBuilder();
        sb.append("[\n");
        for (int i = 0; i < ast.size(); i++) {
            sb.append("  ").append(ast.get(i).toJson());
            if (i < ast.size() - 1) sb.append(",");
            sb.append("\n");
        }
        sb.append("]");
        System.out.println(sb);
    }
}
