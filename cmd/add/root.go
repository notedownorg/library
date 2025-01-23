// Copyright 2024 Notedown Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package add

import (
	"fmt"
	"log/slog"
	"os"

	"github.com/notedownorg/library/pkg/metadata"
	"github.com/notedownorg/library/pkg/notedown"
	"github.com/spf13/cobra"
)

var RootCmd = &cobra.Command{
	Use:   "add <url>",
	Short: "Add a new item to your Notedown library",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		url := args[0]

		format, _, err := metadata.InferFormat(url)
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		title, err := metadata.ExtractTitle(url)
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		ws, err := notedown.DefaultWorkspace()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		client, err := notedown.NewClient(ws)
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		if err = client.CreateSource(title, format, url); err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
		slog.Info("Added source to your workspace", "title", title, "format", format, "url", url)
	},
}
